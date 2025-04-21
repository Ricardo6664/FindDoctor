using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.Entities;
using FindDoctorDomain.ValueObjects;
using FindDoctorDomain.Interfaces;

namespace FindDoctorApplication.Services
{
    public class EstabelecimentoAppService
    {
        private readonly IEstabelecimentoRepository _repo;
        private readonly IGeocodingService _geocoding;

        public EstabelecimentoAppService(IEstabelecimentoRepository repo, IGeocodingService geocoding)
        {
            _repo = repo;
            _geocoding = geocoding;
        }

        public async Task<List<EstabelecimentoDTO>> BuscarProximosAsync(double latitude, double longitude, double raioKm)
        {

            return await _repo.ObterProximosAsync(
                latitude,
                longitude,
                raioKm
            );
        }
    }
}
