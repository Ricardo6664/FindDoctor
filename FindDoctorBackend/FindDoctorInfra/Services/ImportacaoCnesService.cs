using FindDoctorDomain.Entities;
using FindDoctorDomain.Interfaces;
using FindDoctorInfra.Data;
using NetTopologySuite;
using NetTopologySuite.Geometries;
using System;
using System.Collections.Generic;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorInfra.Services
{
    public class ImportacaoCnesService
    {
        private readonly IEnumerable<ICnesCsvProcessor> _processadores;

        public ImportacaoCnesService(IEnumerable<ICnesCsvProcessor> processadores)
        {
            _processadores = processadores;
        }

        public async Task ImportarAsync(CancellationToken cancellationToken)
        {
            //Console.WriteLine("Funcionando");
            // Download OK
            //var zipUrl = "https://cnes.datasus.gov.br/EstatisticasServlet?path=BASE_DE_DADOS_CNES_202502.ZIP"; // URL do CNES
            var tempDir = Path.Combine(Directory.GetCurrentDirectory(), "temp", "cnes");
            //Console.WriteLine(tempDir);
            //Directory.CreateDirectory(tempDir);

            var zipPath = Path.Combine(tempDir, "cnes.zip");

            //using (var client = new HttpClient())
            //{
            //    client.Timeout = TimeSpan.FromMinutes(20);
            //    var bytes = await client.GetByteArrayAsync(zipUrl);
            //    await File.WriteAllBytesAsync(zipPath, bytes, cancellationToken);
            //}


            // Extração OK
            //ZipFile.ExtractToDirectory(zipPath, tempDir, overwriteFiles: true);

            var arquivosImportar = Directory.GetFiles(tempDir, "*.CSV");

            foreach (var processador in _processadores)
            {
                var arquivo = arquivosImportar.FirstOrDefault(a =>
                    Path.GetFileNameWithoutExtension(a).Contains(processador.NomeArquivo, StringComparison.OrdinalIgnoreCase));

                if (arquivo != null)
                {
                    await processador.ProcessarAsync(arquivo, cancellationToken);
                }
            }


            //Directory.Delete(tempDir, recursive: true);
        }
    }
}
