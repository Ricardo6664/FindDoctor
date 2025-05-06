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

        public async Task<List<EstabelecimentoDTO>> ObterProximosAsync(
            double latitude,
            double longitude,
            double raioKm,
            string especialidadeId = null,
            string nomeMedico = null,
            int? convenioId = null
            )
        {
            var pontoReferencia = new Point(longitude, latitude) { SRID = 4326 };


            var sql = new StringBuilder(@"
                SELECT 
                    e.""CodigoCNES"", e.""Nome"", e.""CNPJ"", e.""Endereco"", e.""Numero"", 
                    e.""Bairro"", e.""Cidade"", e.""UF"", e.""Localizacao"", e.""Telefone"",
                    ST_Y(e.""Localizacao""::geometry) AS ""Latitude"",
                    ST_X(e.""Localizacao""::geometry) AS ""Longitude"",
                    p.""CO_Profissional"", p.""Nome"" AS ""NomeProf"", p.""CNS"", p.""SUS"", p.""EspecialidadeId""
                FROM ""Estabelecimentos"" e
                LEFT JOIN ""ProfissionalEstabelecimentos"" pe ON pe.""Id_CNES"" = e.""CodigoUnidade""
                LEFT JOIN ""Profissionais"" p ON p.""CO_Profissional"" = pe.""Id_Profissional""
                ");

                if (convenioId != null)
                {
                    sql.Append(@"
                        INNER JOIN ""EstabelecimentosConvenios"" ec ON ec.""CodigoCNES"" = e.""CodigoUnidade""
                    ");
                }

                sql.Append(@"
                    WHERE ST_DWithin(
                        e.""Localizacao""::geography,
                        ST_SetSRID(ST_MakePoint({0}, {1}), 4326)::geography,
                        {2}
                )
            ");

            if (!string.IsNullOrWhiteSpace(nomeMedico))
            {
                sql.Append(" AND p.\"Nome\" ILIKE {3} ");
            }

            if (!string.IsNullOrWhiteSpace(especialidadeId))
            {
                sql.Append(" AND p.\"EspecialidadeId\" = {4} ");
            }

            if (convenioId != null)
            {
                sql.Append(" AND ec.\"ConvenioId\" = {5} ");
            }

            var parametros = new object[]
            {
                pontoReferencia.X,
                pontoReferencia.Y,
                raioKm * 1000,
                $"%{nomeMedico}%",
                especialidadeId,
                convenioId
            };

            var estabelecimentosComProfissionais = await _db
                .EstabelecimentoComProfissional
                .FromSqlRaw(sql.ToString(), parametros)
                .ToListAsync();

            var resultado = estabelecimentosComProfissionais
                .GroupBy(r => new
                {
                    r.CodigoCNES,
                    r.Nome,
                    r.CNPJ,
                    r.Endereco,
                    r.Numero,
                    r.Bairro,
                    r.Cidade,
                    r.UF,
                    r.Latitude,
                    r.Longitude,
                    r.Telefone
                })
                .Select(g => new EstabelecimentoDTO
                {
                    CodigoCNES = g.Key.CodigoCNES,
                    Nome = g.Key.Nome,
                    CNPJ = g.Key.CNPJ,
                    Endereco = g.Key.Endereco,
                    Numero = g.Key.Numero,
                    Bairro = g.Key.Bairro,
                    Cidade = g.Key.Cidade,
                    UF = g.Key.UF,
                    Latitude = g.Key.Latitude,
                    Longitude = g.Key.Longitude,
                    Telefone = g.Key.Telefone,
                    Profissionais = g
                        .Where(x => x.CO_Profissional != null)
                        .Select(x => new ProfissionalDTO
                        {
                            CO_Profissional = x.CO_Profissional,
                            Nome = x.NomeProf,
                            CNS = x.CNS,
                            SUS = x.SUS,
                            EspecialidadeId = x.EspecialidadeId
                        }).ToList()
                })
                .ToList();

            return resultado;

        }
    }
}
