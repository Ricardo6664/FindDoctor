using Microsoft.EntityFrameworkCore.Design;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorInfra.Data
{
    public class AppDbContextFactory : IDesignTimeDbContextFactory<AppDbContext>
    {
        public AppDbContext CreateDbContext(string[] args)
        {
            var optionsBuilder = new DbContextOptionsBuilder<AppDbContext>();

            // Coloque aqui sua connection string do PostgreSQL
            var connectionString = "Host=db.oluatrgvuqdcaqvkfmjw.supabase.co;Port=5432;Database=postgres;Username=postgres;Password=senhafinddoctor123";

            optionsBuilder.UseNpgsql(connectionString, o => o.UseNetTopologySuite());

            return new AppDbContext(optionsBuilder.Options);
        }
    }
}
