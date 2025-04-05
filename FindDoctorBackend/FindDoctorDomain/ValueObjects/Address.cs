using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FindDoctorDomain.ValueObjects
{
    public class Address
    {
        public string Street { get; set; }
        public string District { get; set; }     
        public string City { get; set; }          
        public string Postcode { get; set; }     // CEP
        public string Country { get; set; }      
        public string County { get; set; } // mesmo nome do campo que volta da photon
        public string State { get; set; }
        public Coordinate Location { get; set; }
    }
}
