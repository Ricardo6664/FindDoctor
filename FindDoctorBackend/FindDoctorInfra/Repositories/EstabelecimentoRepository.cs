using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.Entities;
using FindDoctorDomain.Interfaces;
using FindDoctorDomain.ValueObjects;
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

        public async Task<List<EstabelecimentoDTO>> ObterProximosAsync(double latitude, double longitude, double raioKm)
        {
            var pontoReferencia = new Point(longitude, latitude) { SRID = 4326 };

            return await _db.Estabelecimentos
                .FromSqlInterpolated($@"
                SELECT * FROM ""Estabelecimentos""
                WHERE ST_DWithin(
                    ""Localizacao""::geography,
                    ST_SetSRID(ST_MakePoint({pontoReferencia.X}, {pontoReferencia.Y}), 4326)::geography,
                    {raioKm * 1000}
                )")
                .OrderBy(e => e.Localizacao.Distance(pontoReferencia))
                .Select(e => new EstabelecimentoDTO
                {
                    CodigoCNES = e.CodigoCNES,
                    Nome = e.Nome,
                    CNPJ = e.CNPJ,
                    Endereco = e.Endereco,
                    Numero = e.Numero,
                    Bairro = e.Bairro,
                    Cidade = e.Cidade,
                    UF = e.UF,
                    SUS = e.SUS,
                    Latitude = e.Localizacao.Y,
                    Longitude = e.Localizacao.X,
                    Telefone = e.Telefone
                })
                .ToListAsync();
        }
    }
}
