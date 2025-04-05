using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.ValueObjects;
using FindDoctorDomain.Interfaces;


namespace FindDoctorApplication.Services
{
    public class AddressAppService
    {
        private readonly IGeocodingService _geocodingService;

        public AddressAppService(IGeocodingService geocodingService)
        {
            _geocodingService = geocodingService;
        }

        public async Task<List<Address>> BuscarCoordenadas(string endereco)
        {
            return await _geocodingService.GetCoordinatesAsync(endereco);
        }
    }
}
