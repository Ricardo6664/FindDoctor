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
    public class EspecialidadeCsvProcessor : ICnesCsvProcessor
    {
        private readonly AppDbContext _db;

        public string NomeArquivo => "tbAtividadeProfissional";

        public EspecialidadeCsvProcessor(AppDbContext db)
        {
            _db = db;
        }

        public async Task ProcessarAsync(string caminhoArquivo, CancellationToken cancellationToken)
        {
            using var reader = new StreamReader(caminhoArquivo, Encoding.GetEncoding("ISO-8859-1"));
            
            // Lê o cabeçalho
            var header = reader.ReadLine();
            
            if (header == null) return;

            while (!reader.EndOfStream)
            {
                var linha = reader.ReadLine();
                
                if (string.IsNullOrWhiteSpace(linha)) continue;

                var colunas = linha.Split(';');
                if (colunas.Length < 2) continue;

                var id = colunas[0].Trim('"');
                var nome = colunas[1]?.Trim('"');
                Console.WriteLine(id);
                var especialidade = new Especialidade
                {
                    Id = id,
                    Nome = nome
                };
                
                _db.Especialidades.Add(especialidade);
            }

            await _db.SaveChangesAsync(cancellationToken);

        }
    }
}


