﻿using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NetTopologySuite.Geometries;

namespace FindDoctorDomain.Entities
{
    public class Estabelecimento
    {
        [Key]
        public int CodigoCNES { get; set; }
        public string Nome { get; set; }
        public string CNPJ { get; set; }
        public string Endereco { get; set; }
        public string Numero { get; set; }
        public string Bairro { get; set; }
        public string Cidade { get; set; }
        public string UF { get; set; }
        public bool SUS { get; set; }
        public NetTopologySuite.Geometries.Point Localizacao { get; set; }
        public string Telefone { get; set; }

        public List<HorarioFuncionamento> HorariosFuncionamento { get; set; }
        public List<ProfissionalEstabelecimento> Profissionais { get; set; }
    }
}
