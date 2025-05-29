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


        public async Task<EstabelecimentoDTO> GetById(string codigoCNES)
        {
            return await _repo.GetByIdAsync(codigoCNES);
        }

        public async Task<List<EstabelecimentoDTO>> BuscarProximosAsync(
            double latitude,
            double longitude,
            double raioKm,
            string especialidadeId = null,
            string nomeMedico = null,
            int? convenioId = null
            )
        {

            return await _repo.ObterProximosAsync(
                latitude,
                longitude,
                raioKm,
                especialidadeId,
                nomeMedico,
                convenioId
            );
        }
    }
}
