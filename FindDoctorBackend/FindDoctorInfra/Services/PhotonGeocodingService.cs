using FindDoctorDomain.ValueObjects;
using FindDoctorDomain.Interfaces;
using System.Net.Http;
using System.Text.Json;

namespace FindDoctorInfra.Services
{
    public class PhotonGeocodingService : IGeocodingService
    {
        public async Task<List<Address>> GetCoordinatesAsync(string address)
        {
            using var httpClient = new HttpClient();
            var url = $"https://photon.komoot.io/api/?q={Uri.EscapeDataString(address)}&limit=5";

            var response = await httpClient.GetAsync(url);
            if (!response.IsSuccessStatusCode)
            {
                return new List<Address>();
            }

            var json = await response.Content.ReadAsStringAsync();

            var photonResponse = JsonSerializer.Deserialize<PhotonResponse>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            var result = new List<Address>();

            if (photonResponse?.Features != null)
            {
                foreach (var feature in photonResponse.Features)
                {
                    var coordinates = feature.Geometry.Coordinates;
                    var props = feature.Properties;

                    var addressObj = new Address
                    {
                        Street = props.Street,
                        District = props.District,
                        City = props.City,
                        Postcode = props.Postcode,
                        Country = props.Country,
                        County = props.County,
                        State = props.State,
                        Name  = props.Name,
                        Location = new Coordinate(coordinates[1], coordinates[0])
                    };

                    result.Add(addressObj);
                }
            }

            return result;
        }
    }
}
