using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class Especialidade
    {
        [Key]
        public string Id { get; set; }
        public string Nome { get; set; }

        public List<Profissional> Profissionais { get; set; }
    }
}
