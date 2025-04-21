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

namespace FindDoctorInfra.Processadores
{
    public class ProfissionalCsvProcessor : ICnesCsvProcessor
    {
        private readonly AppDbContext _db;

        public string NomeArquivo => "tbDadosProfissionalSus";

        public ProfissionalCsvProcessor(AppDbContext db)
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
                if (colunas.Length < 11) continue;

                try
                {
                    var coProfissional = colunas[0]?.Trim('"');
                    var nome = colunas[2]?.Trim('"');
                    var cns = colunas[3]?.Trim('"');
                    var sus = false;

                    var profissional = new Profissional
                    {
                        Nome = nome,
                        CNS = cns,
                        SUS = sus,
                        CO_Profissional = coProfissional,
                        EspecialidadeId = null
                    };

                    _db.Profissionais.Add(profissional);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Erro ao processar profissional: {linha}");
                    Console.WriteLine(ex.Message);
                }
            }

            await _db.SaveChangesAsync(cancellationToken);
        }
    }

}
