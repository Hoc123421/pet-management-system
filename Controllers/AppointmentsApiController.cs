using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetManagement.Data;
using PetManagement.Models;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace PetManagement.Controllers
{
    [ApiController]
    [Route("api/appointments")]
    public class AppointmentsApiController : ControllerBase
    {
        private readonly PetDbContext _context;

        public AppointmentsApiController(PetDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> GetAppointments([FromQuery] int? customerId, [FromQuery] string? status)
        {
            var query = _context.Appointments
                .Include(a => a.Pet)
                .Include(a => a.Service)
                .Include(a => a.Customer)
                .AsQueryable();

            if (customerId.HasValue && customerId.Value > 0)
            {
                query = query.Where(a => a.CustomerId == customerId.Value);
            }

            if (!string.IsNullOrWhiteSpace(status) && status != "Tất cả")
            {
                query = query.Where(a => a.Status.ToLower() == status.Trim().ToLower());
            }

            var items = await query.OrderByDescending(a => a.AppointmentDate)
                .Select(a => new
                {
                    a.Id,
                    a.PetId,
                    PetName = a.Pet != null ? a.Pet.Name : "N/A",
                    PetSpecies = a.Pet != null ? a.Pet.Species : "N/A",
                    PetImageUrl = a.Pet != null ? a.Pet.ImageUrl : "",
                    a.ServiceId,
                    ServiceName = a.Service != null ? a.Service.Name : "N/A",
                    a.CustomerId,
                    CustomerName = a.Customer != null ? a.Customer.FullName : "N/A",
                    CustomerPhone = a.Customer != null ? a.Customer.Phone : "N/A",
                    a.AppointmentDate,
                    a.Status,
                    a.Notes,
                    a.TotalPrice,
                    a.CreatedAt
                })
                .ToListAsync();

            return Ok(items);
        }

        [HttpPost]
        public async Task<IActionResult> CreateAppointment([FromBody] AppointmentCreateDto dto, [FromQuery] int customerId = 2)
        {
            var pet = await _context.Pets.FindAsync(dto.PetId);
            var service = await _context.Services.FindAsync(dto.ServiceId);

            if (pet == null || service == null)
            {
                return BadRequest(new { message = "Thú cưng hoặc Dịch vụ không tồn tại!" });
            }

            if (customerId <= 0 || !await _context.Users.AnyAsync(u => u.Id == customerId))
            {
                customerId = pet.OwnerId;
            }

            var appointment = new Appointment
            {
                PetId = dto.PetId,
                ServiceId = dto.ServiceId,
                CustomerId = customerId,
                AppointmentDate = dto.AppointmentDate == default ? DateTime.UtcNow.AddDays(1) : dto.AppointmentDate,
                Status = "Pending",
                Notes = dto.Notes,
                TotalPrice = service.Price,
                CreatedAt = DateTime.UtcNow
            };

            _context.Appointments.Add(appointment);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Đặt lịch hẹn thành công!", appointmentId = appointment.Id });
        }

        [HttpPut("{id}/status")]
        public async Task<IActionResult> UpdateStatus(int id, [FromBody] string status)
        {
            var appointment = await _context.Appointments.FindAsync(id);
            if (appointment == null) return NotFound(new { message = "Không tìm thấy lịch hẹn!" });

            appointment.Status = status;
            await _context.SaveChangesAsync();

            return Ok(new { message = $"Đã cập nhật trạng thái lịch hẹn thành {status}!" });
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> CancelAppointment(int id)
        {
            var appointment = await _context.Appointments.FindAsync(id);
            if (appointment == null) return NotFound(new { message = "Không tìm thấy lịch hẹn!" });

            appointment.Status = "Cancelled";
            await _context.SaveChangesAsync();

            return Ok(new { message = "Đã hủy lịch hẹn thành công!" });
        }
    }
}
