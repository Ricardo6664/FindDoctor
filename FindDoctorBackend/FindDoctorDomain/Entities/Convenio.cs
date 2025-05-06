using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class Convenio
    {
        public int Id { get; set; }
        public string Nome { get; set; }

        public List<EstabelecimentoConvenio> Convenios { get; set; } 

    }
}
