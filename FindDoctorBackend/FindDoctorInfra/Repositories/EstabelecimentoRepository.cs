using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.Entities;
using FindDoctorDomain.Interfaces;
using FindDoctorInfra.Data;
using Microsoft.EntityFrameworkCore;
using NetTopologySuite.Geometries;

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

        public async Task<List<Estabelecimento>> ObterProximosAsync(string cidade, double latitude, double longitude, double raioKm)
        {
            var pontoReferencia = new Point(longitude, latitude) { SRID = 4326 };

            return await _db.Estabelecimentos
                .Where(e => e.Cidade.ToLower() == cidade.ToLower())
                .Where(e => e.Localizacao.IsWithinDistance(pontoReferencia, raioKm * 1000))
                .ToListAsync();
        }
    }
}
