using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PetManagement.Data;
using PetManagement.Models;
using System.Threading.Tasks;

namespace PetManagement.Controllers
{
    [ApiController]
    [Route("api/contact")]
    public class ContactApiController : ControllerBase
    {
        private readonly PetDbContext _context;

        public ContactApiController(PetDbContext context)
        {
            _context = context;
        }

        [HttpPost]
        public async Task<IActionResult> SubmitContact([FromBody] ContactMessage msg)
        {
            if (string.IsNullOrWhiteSpace(msg.Name) || string.IsNullOrWhiteSpace(msg.Email) || string.IsNullOrWhiteSpace(msg.Message))
            {
                return BadRequest(new { message = "Vui lòng điền tên, email và nội dung tin nhắn!" });
            }

            msg.CreatedAt = System.DateTime.UtcNow;
            msg.IsRead = false;
            _context.ContactMessages.Add(msg);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Cảm ơn bạn đã gửi liên hệ! Đội ngũ PetCare sẽ phản hồi sớm nhất." });
        }

        [HttpGet]
        public async Task<IActionResult> GetMessages()
        {
            var msgs = await _context.ContactMessages.OrderByDescending(m => m.CreatedAt).ToListAsync();
            return Ok(msgs);
        }
    }
}
