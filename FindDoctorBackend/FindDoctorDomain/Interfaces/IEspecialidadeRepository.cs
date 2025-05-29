using FindDoctorDomain.Entities;
using FindDoctorDomain.ValueObjects;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Interfaces
{
    public interface IEspecialidadeRepository
    {
        Task<List<Especialidade>> GetAll();
    }
}
