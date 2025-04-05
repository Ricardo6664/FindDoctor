using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.ValueObjects;
namespace FindDoctorDomain.Interfaces
{
    public interface IGeocodingService
    {
        Task<List<Address>> GetCoordinatesAsync(string address);
    }
}
