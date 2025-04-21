using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.Entities
{
    public class HorarioFuncionamento
    {
        public int Id { get; set; }
        public string CodigoCNES { get; set; }
        public int DiaSemanaId { get; set; }
        public TimeOnly HoraInicio { get; set; }
        public TimeOnly HoraFim { get; set; }

        public Estabelecimento Estabelecimento { get; set; }
        public DiaSemana DiaSemana { get; set; }
    }
}
