import pytest
import netCDF4


class TestCloudFractionProcessing:
    product = 'cf'

    @pytest.fixture(autouse=True)
    def _fetch_params(self, params):
        self.full_path = params['full_path']

    @pytest.mark.reprocess
    def test_that_has_correct_attributes(self):
        nc = netCDF4.Dataset(self.full_path)
        assert nc.year == '2019'
        assert nc.month == '05'
        assert nc.day == '17'
        assert nc.title == f'Resampled Cf of ecmwf from Mace-Head'
        assert nc.cloudnet_file_type == "cf_ecmwf"
        assert nc.Conventions == 'CF-1.7'
        nc.close()

    @pytest.mark.reprocess
    @pytest.mark.parametrize("key", [
        'cf_V_ecmwf', 'cf_A_ecmwf', 'cf_V_adv_ecmwf', 'cf_A_adv_ecmwf'])
    def test_that_has_correct_product_variables(self, key):
        nc = netCDF4.Dataset(self.full_path)
        var = nc.variables.keys()
        for v in var:
            if v == key:
                assert True
        nc.close()

    @pytest.mark.reprocess
    @pytest.mark.parametrize("key", [
        'time', 'level', 'latitude', 'longitude', 'horizontal_resolution'])
    def test_that_has_correct_model_variables(self, key):
        nc = netCDF4.Dataset(self.full_path)
        var = nc.variables.keys()
        for v in var:
            if v == key:
                assert True
        nc.close()

    @pytest.mark.reprocess
    @pytest.mark.parametrize("key", [
        'ecmwf_forecast_time', 'ecmwf_height', 'ecmwf_cf'])
    def test_that_has_correct_cycle_variables(self, key):
        nc = netCDF4.Dataset(self.full_path)
        var = nc.variables.keys()
        for v in var:
            if v == key:
                assert True
        nc.close()