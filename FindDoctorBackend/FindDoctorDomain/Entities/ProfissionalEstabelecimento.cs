using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class ProfissionalEstabelecimento
    {
        public int Id_CNES { get; set; }
        public int Id_Profissional { get; set; }

        public Estabelecimento Estabelecimento { get; set; }
        public Profissional Profissional { get; set; }
    }
}
