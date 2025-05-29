using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.ValueObjects
{
    public class ProfissionalDTO
    {
        public string CO_Profissional { get; set; }
        public string Nome { get; set; }
        public string CNS { get; set; }
        public bool? SUS { get; set; }
        public string EspecialidadeNome { get; set; }
    }
}
