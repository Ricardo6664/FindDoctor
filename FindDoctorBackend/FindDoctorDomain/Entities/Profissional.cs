using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class Profissional
    {
        
        [Key]
        public string CO_Profissional { get; set; }

        public string Nome { get; set; }
        public string? EspecialidadeId { get; set; }
        public string CNS { get; set; }
        public bool SUS { get; set; }

        public Especialidade Especialidade { get; set; }
        public List<ProfissionalEstabelecimento> Estabelecimentos { get; set; }
    }
}
