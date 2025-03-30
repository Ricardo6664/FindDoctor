using System.Net;
using Newtonsoft.Json.Linq;

static async Task GetCoords()
{
    Console.Write("Insira seu endereço: ");
    string user_address = Console.ReadLine();

    if (string.IsNullOrEmpty(user_address))
    {
        Console.WriteLine("Address cannot be empty.");
        return;
    }

    string url = $"https://photon.komoot.io/api/?q={Uri.EscapeDataString(user_address)}";

    using (HttpClient client = new HttpClient())
    {
        HttpResponseMessage response = await client.GetAsync(url);

        if (!response.IsSuccessStatusCode)
        {
            Console.WriteLine("Erro ao buscar na API.");
            return;
        }

        string jsonResponse = await response.Content.ReadAsStringAsync();
        JObject json = JObject.Parse(jsonResponse);

        JArray features = (JArray)json["features"];

        if (features.Count == 0)
        {
            Console.WriteLine("Nenhum resultado encontrado.");
            return;
        }

        Console.WriteLine("\nResultados:");
        for (int i = 0; i < features.Count; i++)
        {
            var properties = features[i]["properties"];
            var geometry = features[i]["geometry"];

            string name = properties?["name"]?.ToString() ?? "Unknown";
            string city = properties?["city"]?.ToString() ?? "Unknown";
            string country = properties?["country"]?.ToString() ?? "Unknown";
            double lat = (double)geometry["coordinates"][1];
            double lon = (double)geometry["coordinates"][0];

            Console.WriteLine($"{i + 1}. {name}, {city}, {country} ({lat}, {lon})");
        }
    }
}