using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.Entities;
using FindDoctorDomain.Interfaces;
using FindDoctorInfra.Data;

namespace FindDoctorInfra.Repositories
{
    public class EstabelecimentoRepository : IEstabelecimentoRepository
    {
        private readonly AppDbContext _db;

        public EstabelecimentoRepository(AppDbContext db)
        {
            _db = db;
        }

        public async Task AdicionarAsync(Estabelecimento est, CancellationToken cancellationToken)
        {
            await _db.Estabelecimentos.AddAsync(est, cancellationToken);
        }

        public Task SalvarAsync(CancellationToken cancellationToken)
        {
            return _db.SaveChangesAsync(cancellationToken);
        }
    }
}
