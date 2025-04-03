using Microsoft.AspNetCore.Mvc;
using System.Net;
using System.Dynamic;
using Newtonsoft.Json.Linq;

namespace APITeste.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class TesteController : ControllerBase
    {
        // Marking this as an HTTP GET action to avoid ambiguity for Swagger
        [HttpGet("address")]
        public async Task<IActionResult> GetAddress(string user_address)
        {
            string url = $"https://photon.komoot.io/api/?q={Uri.EscapeDataString(user_address)}";

            using (HttpClient client = new HttpClient())
            {
                HttpResponseMessage response = await client.GetAsync(url);

                if (!response.IsSuccessStatusCode)
                {
                    // Handle the error if request fails
                    return StatusCode((int)response.StatusCode, "Error fetching address data.");
                }

                string jsonResponse = await response.Content.ReadAsStringAsync();
                JObject json = JObject.Parse(jsonResponse);

                JArray features = (JArray)json["features"];

                List<ExpandoObject> retornos = new List<ExpandoObject>();
                if (features.Count > 0)
                {
                    for (int i = 0; i < features.Count; i++)

                    {
                        dynamic retorno = new ExpandoObject();

                        var properties = features[0]["properties"];
                        var geometry = features[0]["geometry"];

                        retorno.name = properties?["name"]?.ToString() ?? "Unknown";
                        retorno.city = properties?["city"]?.ToString() ?? "Unknown";
                        retorno.state = properties?["state"]?.ToString() ?? "Unknown";
                        retorno.street = properties?["street"]?.ToString() ?? "Unknown";
                        retorno.country = properties?["country"]?.ToString() ?? "Unknown";
                        retorno.lat = (double)geometry["coordinates"][1];
                        retorno.lon = (double)geometry["coordinates"][0];
                        retornos.Add(retorno);
                    }
                }

                return Ok(retornos);
            }
        }

        // This method calls GetAddress but is clearly marked as an HTTP GET method
        [HttpGet(Name = "GetEndereco")]
        public async Task<IActionResult> Get(string user_address)
        {
            return await GetAddress(user_address);
        }
    }
}
