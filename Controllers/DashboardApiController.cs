using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetManagement.Data;
using System.Linq;
using System.Threading.Tasks;

namespace PetManagement.Controllers
{
    [ApiController]
    [Route("api/dashboard")]
    public class DashboardApiController : ControllerBase
    {
        private readonly PetDbContext _context;

        public DashboardApiController(PetDbContext context)
        {
            _context = context;
        }

        [HttpGet("stats")]
        public async Task<IActionResult> GetStats()
        {
            int totalPets = await _context.Pets.CountAsync();
            int totalAppointments = await _context.Appointments.CountAsync();
            int pendingAppointments = await _context.Appointments.CountAsync(a => a.Status == "Pending");
            int totalProducts = await _context.Products.CountAsync();
            int totalUsers = await _context.Users.CountAsync();
            decimal appointmentRevenue = await _context.Appointments
                .Where(a => a.Status == "Completed")
                .SumAsync(a => (decimal?)a.TotalPrice) ?? 0;

            decimal productRevenue = await _context.ProductOrders
                .Where(o => o.Status == "Completed")
                .SumAsync(o => (decimal?)o.TotalAmount) ?? 0;

            decimal totalRevenue = appointmentRevenue + productRevenue;




            var recentAppointments = await _context.Appointments
                .Include(a => a.Pet)
                .Include(a => a.Service)
                .Include(a => a.Customer)
                .OrderByDescending(a => a.CreatedAt)
                .Take(5)
                .Select(a => new
                {
                    a.Id,
                    PetName = a.Pet != null ? a.Pet.Name : "N/A",
                    ServiceName = a.Service != null ? a.Service.Name : "N/A",
                    CustomerName = a.Customer != null ? a.Customer.FullName : "N/A",
                    a.AppointmentDate,
                    a.Status,
                    a.TotalPrice
                })
                .ToListAsync();

            return Ok(new
            {
                totalPets,
                totalAppointments,
                pendingAppointments,
                totalProducts,
                totalUsers,
                totalRevenue,
                recentAppointments
            });
        }
    }
}
