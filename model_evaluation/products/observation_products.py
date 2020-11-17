import numpy as np
import numpy.ma as ma
from datetime import datetime
from cloudnetpy import utils
from cloudnetpy.categorize.datasource import DataSource
from cloudnetpy.products.product_tools import CategorizeBits


class ObservationManager(DataSource):
    """Class to collect and manage observations for downsampling.

        Args:
            obs (str): Name of observation product
            obs_file (DataSource): The :class:'DataSource' instance

        Notes:
            Output is ObservationManager object where all product data and
            information is included.

            Class inherits DataSource interface from CloudnetPy. Observation file
            should be processed using CloudnetPy for this class to work properly.
    """
    def __init__(self, obs, obs_file):
        super().__init__(obs_file)
        self.obs = obs
        self._file = obs_file
        self.date = self._get_date()
        self._generate_product()

    def _get_date(self):
        """Returns measurement date as datetime."""
        return datetime(int(self.dataset.year), int(self.dataset.month),
                        int(self.dataset.day), 0, 0, 0)

    def _generate_product(self):
        """Add all needed of observations to object"""
        if self.obs == 'cf':
            self.append_data(self._generate_cf(), 'cf')
        else:
            self.append_data(self.getvar(self.obs), self.obs)
            if self.obs == 'iwc':
                self._generate_iwc_masks()
        self.append_data(self.getvar('height'), 'height')

    def _generate_cf(self):
        """Generates cloud fractions using categorize bits and masking conditions"""
        categorize_bits = CategorizeBits(self._file)
        cloud_mask = self._classify_basic_mask(categorize_bits.category_bits)
        cloud_mask = self._mask_cloud_bits(cloud_mask)
        if self._check_rainrate():
            cloud_mask[~self._rain_index(), :] = ma.masked
        return cloud_mask

    def _classify_basic_mask(self, bits):
        cloud_mask = bits['droplet'] + bits['falling'] * 2
        cloud_mask[bits['falling'] & bits['cold']] = cloud_mask[bits['falling'] & bits['cold']] + 2
        cloud_mask[bits['aerosol']] = 6
        cloud_mask[bits['insect']] = 7
        cloud_mask[bits['aerosol'] & bits['insect']] = 8
        return cloud_mask

    def _mask_cloud_bits(self, cloud_mask):
        """Creates cloud fraction"""
        for i in [1, 3, 4, 5]:
            cloud_mask[cloud_mask == i] = 1
        for i in [2, 6, 7, 8]:
            cloud_mask[cloud_mask == i] = 0
        return cloud_mask

    def _check_rainrate(self):
        """Check if rainrate in file"""
        try:
            self.getvar('rainrate')
            return True
        except RuntimeError:
            return False

    def _get_rainrate_threshold(self):
        wband = utils.get_wl_band(self.getvar('radar_frequency'))
        rainrate_threshold = 8
        if 90 < wband < 100:
            rainrate_threshold = 2
        return rainrate_threshold

    def _rain_index(self):
        rainrate = self.getvar('rainrate')
        rainrate_threshold = self._get_rainrate_threshold()
        return rainrate > rainrate_threshold

    def _generate_iwc_masks(self):
        """Generates ice water content variables with different masks"""
        #TODO: Differences with CloudnetPy (status=2) and Legacy data (status=3)
        iwc = self.getvar(self.obs)
        iwc_status = self.getvar('iwc_retrieval_status')
        self._mask_iwc_att(iwc, iwc_status)
        self._get_rain_iwc(iwc_status.data)
        self._mask_iwc(iwc, iwc_status)

    def _mask_iwc(self, iwc, iwc_status):
        """Leaves only data of reliable data and corrected liquid attenuation"""
        iwc_mask = ma.copy(iwc)
        iwc_mask[np.bitwise_and(iwc_status != 1, iwc_status != 2)] = ma.masked
        self.append_data(iwc, 'iwc')

    def _mask_iwc_att(self, iwc, iwc_status):
        """Leaves only data where is reliable data, corrected liquid attenuation
        and uncorrected liquid attenuation"""
        iwc_att = ma.copy(iwc)
        iwc_att[iwc_status > 3] = ma.masked
        self.append_data(iwc_att, 'iwc_att')

    def _get_rain_iwc(self, iwc_status):
        """Finds columns where is rain, return boolean of x-axis shape"""
        iwc_rain = np.zeros(iwc_status.shape, dtype=bool)
        iwc_rain[iwc_status == 5] = 1
        iwc_rain = np.any(iwc_rain, axis=1)
        self.append_data(iwc_rain, 'iwc_rain')
