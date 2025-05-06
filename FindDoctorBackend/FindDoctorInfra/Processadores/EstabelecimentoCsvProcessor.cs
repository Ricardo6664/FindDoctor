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
using System.Globalization;

namespace FindDoctorInfra.Processadores
{
    public class EstabelecimentoCsvProcessor : ICnesCsvProcessor
    {
        private readonly AppDbContext _db;
        private readonly GeometryFactory _geometryFactory;

        public string NomeArquivo => "tbEstabelecimento";

        public EstabelecimentoCsvProcessor(AppDbContext db)
        {
            _db = db;
            _geometryFactory = NtsGeometryServices.Instance.CreateGeometryFactory(srid: 4326);
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
                if (colunas.Length < 44) continue;


                try
                {
                    var latitudeStr = colunas[39]?.Trim('"').Trim();
                    var longitudeStr = colunas[40]?.Trim('"').Trim();

                    var latitude = double.TryParse(latitudeStr, NumberStyles.Any, CultureInfo.InvariantCulture, out var lat) ? lat : 0;
                    var longitude = double.TryParse(longitudeStr, NumberStyles.Any, CultureInfo.InvariantCulture, out var lng) ? lng : 0;

                    var estabelecimento = new Estabelecimento
                    {
                        CodigoUnidade = colunas[0]?.Trim('"'),
                        CodigoCNES = colunas[1]?.Trim('"'),
                        CNPJ = colunas[20]?.Trim('"'),
                        Nome = colunas[6]?.Trim('"'),
                        Endereco = colunas[7]?.Trim('"'),
                        Numero = colunas[8]?.Trim('"'),
                        Bairro = colunas[10]?.Trim('"'),
                        Cidade = colunas[31]?.Trim('"'),
                        UF = colunas[30]?.Trim('"'),
                        Telefone = colunas[16]?.Trim('"'),
                        Localizacao = _geometryFactory.CreatePoint(new Coordinate(longitude, latitude))
                    };

                    _db.Estabelecimentos.Add(estabelecimento);
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
