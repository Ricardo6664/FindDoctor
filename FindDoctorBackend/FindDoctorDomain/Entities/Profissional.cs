using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class Profissional
    {
        public int Id { get; set; }
        public string Nome { get; set; }
        public int? EspecialidadeId { get; set; }
        public string CNS { get; set; }
        public bool SUS { get; set; }

        public Especialidade Especialidade { get; set; }
        public List<ProfissionalEstabelecimento> Estabelecimentos { get; set; }
    }
}
