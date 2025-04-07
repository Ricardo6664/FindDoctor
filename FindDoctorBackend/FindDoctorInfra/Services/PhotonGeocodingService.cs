using FindDoctorDomain.ValueObjects;
using FindDoctorDomain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Net.WebRequestMethods;

namespace FindDoctorInfra.Services
{
    class PhotonGeocodingService : IGeocodingService
    {
        public Task<List<Address>> GetCoordinatesAsync(string address) {
            return Task.FromResult(new List<Address>());
        }
    }
}
