using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class ProfissionalEstabelecimento
    {
        public string Id_CNES { get; set; }
        public string Id_Profissional { get; set; }
        public string? EspecialidadeId { get; set; }
        public Estabelecimento Estabelecimento { get; set; }
        public Profissional Profissional { get; set; }
    }
}
