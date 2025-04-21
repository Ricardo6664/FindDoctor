using FindDoctorDomain.Entities;
using FindDoctorDomain.Interfaces;
using FindDoctorInfra.Data;
using NetTopologySuite.Geometries;
using NetTopologySuite;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace FindDoctorInfra.Processadores
{
    public class ProfissionalEstabelecimentoCsvProcessor : ICnesCsvProcessor
    {
        private readonly AppDbContext _db;

        public string NomeArquivo => "rlEstabEquipeProf";

        public ProfissionalEstabelecimentoCsvProcessor(AppDbContext db)
        {
            _db = db;
        }

        public async Task ProcessarAsync(string caminhoArquivo, CancellationToken cancellationToken)
        {
            using var reader = new StreamReader(caminhoArquivo, Encoding.GetEncoding("ISO-8859-1"));

            var header = reader.ReadLine();

            while (!reader.EndOfStream)
            {
                var linha = reader.ReadLine();
                if (string.IsNullOrWhiteSpace(linha)) continue;

                var colunas = linha.Split(';');

                try
                {
                    var coProfissionalSus = colunas[3].Trim('"'); // CO_PROFISSIONAL_SUS
                    var coCbo = colunas[5].Trim('"');             // CO_CBO
                    var coUnidade = colunas[4].Trim('"');         // CO_UNIDADE

                    var jaRastreado = _db.ChangeTracker.Entries<ProfissionalEstabelecimento>()
                                .Any(e => e.Entity.Id_CNES == coUnidade && e.Entity.Id_Profissional == coProfissionalSus);


                    if (!jaRastreado)
                    {
                        
                        var vinculo = new ProfissionalEstabelecimento
                        {
                            Id_CNES = coUnidade,
                            Id_Profissional = coProfissionalSus,
                            EspecialidadeId = coCbo
                        };

                        _db.ProfissionalEstabelecimentos.Add(vinculo);
                    }
                    
                    
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Erro ao processar linha: {linha}");
                    Console.WriteLine(ex.Message);
                }
            }


            await _db.SaveChangesAsync(cancellationToken);
        }
    }

}
