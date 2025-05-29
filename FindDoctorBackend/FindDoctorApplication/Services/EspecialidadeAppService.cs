using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using FindDoctorDomain.Entities;
using FindDoctorDomain.ValueObjects;
using FindDoctorDomain.Interfaces;

namespace FindDoctorApplication.Services
{
    public class EspecialidadeAppService
    {
        private readonly IEspecialidadeRepository _repo;

        public EspecialidadeAppService(IEspecialidadeRepository repo)
        {
            _repo = repo;
        }

        public Task<List<Especialidade>> GetAll()
        {

            return _repo.GetAll();
        }
    }
}
