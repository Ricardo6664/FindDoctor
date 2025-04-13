using System.Collections.Generic;
using System.Text.Json.Serialization;

public class PhotonResponse
{
    [JsonPropertyName("features")]
    public List<PhotonFeature> Features { get; set; }
}

public class PhotonFeature
{
    [JsonPropertyName("geometry")]
    public PhotonGeometry Geometry { get; set; }

    [JsonPropertyName("properties")]
    public PhotonProperties Properties { get; set; }
}

public class PhotonGeometry
{
    [JsonPropertyName("coordinates")]
    public List<double> Coordinates { get; set; }
}

public class PhotonProperties
{
    [JsonPropertyName("street")]
    public string Street { get; set; }

    [JsonPropertyName("district")]
    public string District { get; set; }

    [JsonPropertyName("city")]
    public string City { get; set; }

    [JsonPropertyName("postcode")]
    public string Postcode { get; set; }

    [JsonPropertyName("country")]
    public string Country { get; set; }

    [JsonPropertyName("county")]
    public string County { get; set; }

    [JsonPropertyName("state")]
    public string State { get; set; }

    [JsonPropertyName("name")]
    public string Name { get; set; }

}
