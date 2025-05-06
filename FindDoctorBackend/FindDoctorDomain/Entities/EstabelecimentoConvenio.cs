using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class EstabelecimentoConvenio
    {
        public string CodigoCNES { get; set; }
        public int ConvenioId { get; set; }

        public Estabelecimento Estabelecimento { get; set; }
        public Convenio Convenio { get; set; }
    }
}
