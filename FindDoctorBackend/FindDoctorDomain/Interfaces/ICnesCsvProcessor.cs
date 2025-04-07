using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Interfaces
{
    public interface ICnesCsvProcessor
    {
        string NomeArquivo { get; } 
        Task ProcessarAsync(string caminhoArquivo, CancellationToken cancellationToken);
    }
}
