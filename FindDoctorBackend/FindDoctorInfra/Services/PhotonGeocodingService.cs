using FindDoctorDomain.ValueObjects;
using FindDoctorDomain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorInfra.Services
{
    class PhotonGeocodingService : IGeocodingService
    {
        public Task<List<Address>> GetCoordinatesAsync(string address) { }
    }
}
