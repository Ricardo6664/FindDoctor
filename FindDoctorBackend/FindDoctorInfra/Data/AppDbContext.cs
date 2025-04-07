using FindDoctorDomain.Entities;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
namespace FindDoctorInfra.Data
{
    public class AppDbContext : DbContext
    {
        public DbSet<Estabelecimento> Estabelecimentos { get; set; }
        public DbSet<HorarioFuncionamento> HorariosFuncionamento { get; set; }
        public DbSet<DiaSemana> DiasSemana { get; set; }
        public DbSet<Profissional> Profissionais { get; set; }
        public DbSet<Especialidade> Especialidades { get; set; }
        public DbSet<ProfissionalEstabelecimento> ProfissionalEstabelecimentos { get; set; }

        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }


        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            // 🧪 Connection string direta aqui só pra teste
            optionsBuilder.UseNpgsql("Host=localhost;Port=5432;Database=finddoctor;Username=postgres;Password=senha");
        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Estabelecimento>(entity =>
            {
                entity.HasKey(e => e.CodigoCNES);

                entity.Property(e => e.Localizacao)
                      .HasColumnType("geometry (point)");
            });


            modelBuilder.Entity<ProfissionalEstabelecimento>()
                .HasKey(pe => new { pe.Id_CNES, pe.Id_Profissional });

            modelBuilder.Entity<ProfissionalEstabelecimento>()
                .HasOne(pe => pe.Estabelecimento)
                .WithMany(e => e.Profissionais)
                .HasForeignKey(pe => pe.Id_CNES);

            modelBuilder.Entity<ProfissionalEstabelecimento>()
                .HasOne(pe => pe.Profissional)
                .WithMany(p => p.Estabelecimentos)
                .HasForeignKey(pe => pe.Id_Profissional);

            modelBuilder.Entity<HorarioFuncionamento>()
                .HasOne(h => h.Estabelecimento)
                .WithMany(e => e.HorariosFuncionamento)
                .HasForeignKey(h => h.CodigoCNES);

            modelBuilder.Entity<HorarioFuncionamento>()
                .HasOne(h => h.DiaSemana)
                .WithMany(d => d.Horarios)
                .HasForeignKey(h => h.DiaSemanaId);

            modelBuilder.Entity<Profissional>()
                .HasOne(p => p.Especialidade)
                .WithMany(e => e.Profissionais)
                .HasForeignKey(p => p.EspecialidadeId)
                .IsRequired(false);
        }
    }

}
