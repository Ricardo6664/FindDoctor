using FindDoctorDomain.Entities;
using FindDoctorDomain.ValueObjects;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Interfaces
{
    public interface IEstabelecimentoRepository
    {
        Task AdicionarAsync(Estabelecimento est, CancellationToken cancellationToken);
        Task SalvarAsync(CancellationToken cancellationToken);
        Task<EstabelecimentoDTO> GetByIdAsync(string codigoCNES);
        Task<List<EstabelecimentoDTO>> ObterProximosAsync(
            double latitude,
            double longitude,
            double raioKm,
            string especialidadeId = null,
            string nomeMedico = null,
            int? convenioId = null
        );
    }
}
