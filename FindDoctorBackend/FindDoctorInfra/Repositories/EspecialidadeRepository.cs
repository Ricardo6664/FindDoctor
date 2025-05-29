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
    public class EspecialidadeRepository : IEspecialidadeRepository
    {
        private readonly AppDbContext _db;

        public EspecialidadeRepository(AppDbContext db)
        {
            _db = db;
        }

        public Task<List<Especialidade>> GetAll()
        {
            return _db.Especialidades.ToListAsync();
        }

    }
}
