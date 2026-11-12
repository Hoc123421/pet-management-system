using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Google.Apis.Auth;
using PetManagement.Data;
using PetManagement.Models;
using System;
using System.Threading.Tasks;

namespace PetManagement.Controllers
{
    [ApiController]
    [Route("api/auth")]
    public class AuthApiController : ControllerBase
    {
        private readonly PetDbContext _context;
        private readonly IConfiguration _configuration;

        public AuthApiController(PetDbContext context, IConfiguration configuration)
        {
            _context = context;
            _configuration = configuration;
        }


        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginDto dto)
        {
            if (string.IsNullOrWhiteSpace(dto.Email) || string.IsNullOrWhiteSpace(dto.Password))
            {
                return BadRequest(new { message = "Vui lòng nhập Email và Mật khẩu!" });
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email.ToLower() == dto.Email.ToLower());
            if (user == null || user.PasswordHash != dto.Password)
            {
                return Unauthorized(new { message = "Email hoặc mật khẩu không chính xác!" });
            }

            // Generate token string (Simple token for educational/demo project)
            string token = $"DEMO_JWT_TOKEN_ROLE_{user.Role}_{user.Id}_{Guid.NewGuid()}";

            // Also set HTTP Cookie for Session Auth requirement
            Response.Cookies.Append("AuthToken", token, new CookieOptions
            {
                HttpOnly = true,
                Expires = DateTimeOffset.UtcNow.AddDays(7),
                SameSite = SameSiteMode.Lax
            });

            return Ok(new AuthResponseDto
            {
                Token = token,
                User = MapToUserDto(user)
            });
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterDto dto)
        {
            if (string.IsNullOrWhiteSpace(dto.Email) || string.IsNullOrWhiteSpace(dto.Password) || string.IsNullOrWhiteSpace(dto.FullName))
            {
                return BadRequest(new { message = "Vui lòng nhập đầy đủ thông tin bắt buộc!" });
            }

            var existingUser = await _context.Users.FirstOrDefaultAsync(u => u.Email.ToLower() == dto.Email.ToLower());
            if (existingUser != null)
            {
                return BadRequest(new { message = "Email này đã được sử dụng!" });
            }

            var newUser = new User
            {
                FullName = dto.FullName,
                Email = dto.Email,
                PasswordHash = dto.Password,
                Phone = dto.Phone,
                Address = dto.Address,
                Role = string.Equals(dto.Role, "Admin", StringComparison.OrdinalIgnoreCase) ? "Admin" : "Customer",
                AvatarUrl = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200&auto=format&fit=crop",
                OAuthProvider = "Local",
                CreatedAt = DateTime.UtcNow
            };

            _context.Users.Add(newUser);
            await _context.SaveChangesAsync();

            string token = $"DEMO_JWT_TOKEN_ROLE_{newUser.Role}_{newUser.Id}_{Guid.NewGuid()}";

            return Ok(new AuthResponseDto
            {
                Token = token,
                User = MapToUserDto(newUser)
            });
        }

        [HttpGet("google-config")]
        public IActionResult GetGoogleConfig()
        {
            string clientId = _configuration["Authentication:Google:ClientId"] ?? string.Empty;
            bool isConfigured = !string.IsNullOrWhiteSpace(clientId) && !clientId.Contains("YOUR_GOOGLE_CLIENT_ID");
            return Ok(new { clientId = clientId, isConfigured = isConfigured });
        }

        [HttpPost("google-login")]
        public async Task<IActionResult> GoogleLogin([FromBody] GoogleJwtLoginDto dto)
        {
            if (string.IsNullOrWhiteSpace(dto.IdToken))
            {
                return BadRequest(new { message = "IdToken Google không được để trống!" });
            }

            try
            {
                string expectedClientId = _configuration["Authentication:Google:ClientId"] ?? string.Empty;
                
                var settings = new GoogleJsonWebSignature.ValidationSettings();
                if (!string.IsNullOrWhiteSpace(expectedClientId) && !expectedClientId.Contains("YOUR_GOOGLE_CLIENT_ID"))
                {
                    settings.Audience = new[] { expectedClientId };
                }

                GoogleJsonWebSignature.Payload payload = await GoogleJsonWebSignature.ValidateAsync(dto.IdToken, settings);
                
                if (payload == null || string.IsNullOrWhiteSpace(payload.Email))
                {
                    return BadRequest(new { message = "Google ID Token không hợp lệ!" });
                }

                var user = await _context.Users.FirstOrDefaultAsync(u => u.Email.ToLower() == payload.Email.ToLower());
                if (user == null)
                {
                    user = new User
                    {
                        FullName = payload.Name ?? "Google User",
                        Email = payload.Email,
                        PasswordHash = "GOOGLE_OAUTH2_AUTHENTICATED",
                        Role = "Customer",
                        AvatarUrl = payload.Picture ?? "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop",
                        OAuthProvider = "Google",
                        CreatedAt = DateTime.UtcNow
                    };

                    _context.Users.Add(user);
                    await _context.SaveChangesAsync();
                }
                else
                {
                    if (!string.IsNullOrWhiteSpace(payload.Picture)) user.AvatarUrl = payload.Picture;
                    if (!string.IsNullOrWhiteSpace(payload.Name) && (user.FullName == "OAuth User" || user.FullName == "Người Dùng Google"))
                    {
                        user.FullName = payload.Name;
                    }
                    await _context.SaveChangesAsync();
                }

                string token = $"GOOGLE_OAUTH2_JWT_ROLE_{user.Role}_{user.Id}_{Guid.NewGuid()}";

                Response.Cookies.Append("AuthToken", token, new CookieOptions
                {
                    HttpOnly = true,
                    Expires = DateTimeOffset.UtcNow.AddDays(7),
                    SameSite = SameSiteMode.Lax
                });

                return Ok(new AuthResponseDto
                {
                    Token = token,
                    User = MapToUserDto(user)
                });
            }
            catch (InvalidJwtException ex)
            {
                return BadRequest(new { message = $"Xác thực Google ID Token thất bại: {ex.Message}" });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { message = $"Lỗi xử lý đăng nhập Google: {ex.Message}" });
            }
        }

        [HttpPost("oauth2-login")]
        public async Task<IActionResult> OAuth2Login([FromBody] OAuth2LoginDto dto)
        {
            if (string.IsNullOrWhiteSpace(dto.Email))
            {
                return BadRequest(new { message = "Vui lòng cung cấp Email OAuth2!" });
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email.ToLower() == dto.Email.ToLower());
            if (user == null)
            {
                user = new User
                {
                    FullName = string.IsNullOrWhiteSpace(dto.FullName) ? "OAuth User" : dto.FullName,
                    Email = dto.Email,
                    PasswordHash = "OAUTH2_EXTERNAL_USER",
                    Role = "Customer",
                    AvatarUrl = string.IsNullOrWhiteSpace(dto.AvatarUrl) 
                        ? "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&auto=format&fit=crop" 
                        : dto.AvatarUrl,
                    OAuthProvider = dto.Provider ?? "Google",
                    CreatedAt = DateTime.UtcNow
                };

                _context.Users.Add(user);
                await _context.SaveChangesAsync();
            }

            string token = $"OAUTH2_JWT_TOKEN_ROLE_{user.Role}_{user.Id}_{Guid.NewGuid()}";

            Response.Cookies.Append("AuthToken", token, new CookieOptions
            {
                HttpOnly = true,
                Expires = DateTimeOffset.UtcNow.AddDays(7),
                SameSite = SameSiteMode.Lax
            });

            return Ok(new AuthResponseDto
            {
                Token = token,
                User = MapToUserDto(user)
            });
        }


        [HttpGet("me")]
        public async Task<IActionResult> GetCurrentUser([FromQuery] int userId)
        {
            var user = await _context.Users.FindAsync(userId);
            if (user == null) return NotFound(new { message = "Không tìm thấy người dùng!" });
            return Ok(MapToUserDto(user));
        }

        [HttpPost("logout")]
        public IActionResult Logout()
        {
            Response.Cookies.Delete("AuthToken");
            return Ok(new { message = "Đã đăng xuất thành công!" });
        }

        private static UserDto MapToUserDto(User u)
        {
            return new UserDto
            {
                Id = u.Id,
                FullName = u.FullName,
                Email = u.Email,
                Role = u.Role,
                Phone = u.Phone,
                Address = u.Address,
                AvatarUrl = u.AvatarUrl,
                OAuthProvider = u.OAuthProvider
            };
        }
    }
}
