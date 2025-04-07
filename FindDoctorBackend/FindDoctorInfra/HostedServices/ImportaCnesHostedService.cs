using FindDoctorInfra.Services;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;

namespace FindDoctorInfra.HostedServices
{
    public class ImportaCnesHostedService : BackgroundService
    {
        private readonly IServiceProvider _provider;

        public ImportaCnesHostedService(IServiceProvider provider)
        {
            _provider = provider;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            Console.WriteLine("HostedService começou");
            using var scope = _provider.CreateScope();
            var service = scope.ServiceProvider.GetRequiredService<ImportacaoCnesService>();

            // roda só uma vez (ex: no startup)
            await service.ImportarAsync(stoppingToken);
        }
    }
}
