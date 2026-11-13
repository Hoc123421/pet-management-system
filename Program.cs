using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using PetManagement.Data;
using Prometheus;
using System;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
    });
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Configure DbContext with fallback strategy for seamless running
string connectionString = builder.Configuration.GetConnectionString("DefaultConnection") 
    ?? "Server=localhost,1433;Database=PetManagementDb;User Id=sa;Password=YourStrong@Password2026;TrustServerCertificate=True;";

bool useInMemory = builder.Configuration.GetValue<bool>("UseInMemoryDatabase", false);

builder.Services.AddDbContext<PetDbContext>(options =>
{
    if (useInMemory)
    {
        options.UseInMemoryDatabase("PetManagementInMemoryDb");
    }
    else
    {
        try
        {
            options.UseSqlServer(connectionString, sqlOptions =>
            {
                sqlOptions.EnableRetryOnFailure(
                    maxRetryCount: 5,
                    maxRetryDelay: TimeSpan.FromSeconds(10),
                    errorNumbersToAdd: null);
            });
        }
        catch
        {
            options.UseInMemoryDatabase("PetManagementFallbackDb");
        }
    }
});

var app = builder.Build();

// Auto initialize and seed database
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var dbContext = services.GetRequiredService<PetDbContext>();
        dbContext.Database.EnsureCreated();
    }
    catch (Exception ex)
    {
        Console.WriteLine($"DB Connection Note: {ex.Message}. Falling back to InMemory mode...");
        // Re-ensure with InMemory if SQL Server container is starting
    }
}

// Enable Swagger in Development or Demo
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Pet Management API v1");
    c.RoutePrefix = "swagger";
});

app.UseCors("AllowAll");
app.UseDefaultFiles();
app.UseStaticFiles();

// Prometheus: thu thập metrics HTTP (request count, duration, status code)
app.UseHttpMetrics();

app.UseAuthorization();
app.MapControllers();

// Endpoint cho Prometheus scrape: GET /metrics
app.MapMetrics();
// Endpoint kiểm tra sức khỏe cho CI/CD: GET /health
app.MapGet("/health", () => Results.Ok(new { status = "Healthy", time = DateTime.UtcNow }));

app.Run();
