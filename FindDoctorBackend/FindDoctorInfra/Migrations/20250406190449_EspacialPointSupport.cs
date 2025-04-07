using Microsoft.EntityFrameworkCore.Migrations;
using NetTopologySuite.Geometries;

#nullable disable

namespace FindDoctorInfra.Migrations
{
    /// <inheritdoc />
    public partial class EspacialPointSupport : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterDatabase()
                .Annotation("Npgsql:PostgresExtension:postgis", ",,");

            migrationBuilder.AlterColumn<Point>(
                name: "Localizacao",
                table: "Estabelecimentos",
                type: "geometry (point)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "text");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterDatabase()
                .OldAnnotation("Npgsql:PostgresExtension:postgis", ",,");

            migrationBuilder.AlterColumn<string>(
                name: "Localizacao",
                table: "Estabelecimentos",
                type: "text",
                nullable: false,
                oldClrType: typeof(Point),
                oldType: "geometry (point)");
        }
    }
}
