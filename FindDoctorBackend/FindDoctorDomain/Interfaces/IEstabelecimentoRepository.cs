using FindDoctorDomain.Entities;
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
    }
}
