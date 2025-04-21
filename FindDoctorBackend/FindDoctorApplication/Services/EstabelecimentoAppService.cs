using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.Entities;
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

        public async Task<List<Estabelecimento>> BuscarProximosAsync(string endereco, double raioKm)
        {
            var coordenadas = await _geocoding.GetCoordinatesAsync(endereco);

            if (!coordenadas.Any())
                return new List<Estabelecimento>();

            var primeria = coordenadas.First();
            var cidade = primeria.City;

            return await _repo.ObterProximosAsync(
                cidade,
                primeria.Location.Latitude,
                primeria.Location.Longitude,
                raioKm
            );
        }
    }
}
