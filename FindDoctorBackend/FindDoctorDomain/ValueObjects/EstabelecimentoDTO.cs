using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.ValueObjects
{
    public class EstabelecimentoDTO
    {
        public string CodigoCNES { get; set; }
        public string Nome { get; set; }
        public string CNPJ { get; set; }
        public string Endereco { get; set; }
        public string Numero { get; set; }
        public string Bairro { get; set; }
        public string Cidade { get; set; }
        public string UF { get; set; }
        public double Latitude { get; set; }
        public double Longitude { get; set; }
        public string Telefone { get; set; }
        
        public List<ProfissionalDTO> Profissionais { get; set; }
    }
}
