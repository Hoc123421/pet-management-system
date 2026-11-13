using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace PetManagement.Models
{
    public class User
    {
        public int Id { get; set; }
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string PasswordHash { get; set; } = string.Empty;
        public string Role { get; set; } = "Customer"; // Admin, Staff, Customer
        public string Phone { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public string AvatarUrl { get; set; } = string.Empty;
        public string OAuthProvider { get; set; } = "Local"; // Local, Google
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        [JsonIgnore]
        public ICollection<Pet> Pets { get; set; } = new List<Pet>();
        [JsonIgnore]
        public ICollection<Appointment> Appointments { get; set; } = new List<Appointment>();
    }

    public class Pet
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Species { get; set; } = "Chó"; // Chó, Mèo, Thỏ, Chim, Khác
        public string Breed { get; set; } = string.Empty;
        public int AgeYears { get; set; }
        public double WeightKg { get; set; }
        public string Gender { get; set; } = "Đực"; // Đực, Cái
        public string HealthNotes { get; set; } = string.Empty;
        public string ImageUrl { get; set; } = string.Empty;
        public int OwnerId { get; set; }
        [JsonIgnore]
        public User? Owner { get; set; }
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        [JsonIgnore]
        public ICollection<Appointment> Appointments { get; set; } = new List<Appointment>();
    }

    public class PetService
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Category { get; set; } = "Spa & Grooming";
        public decimal Price { get; set; }
        public int DurationMinutes { get; set; } = 45;
        public string Description { get; set; } = string.Empty;
        public string ImageUrl { get; set; } = string.Empty;
        public bool IsActive { get; set; } = true;

        public ICollection<Appointment> Appointments { get; set; } = new List<Appointment>();
    }

    public class Appointment
    {
        public int Id { get; set; }
        public int PetId { get; set; }
        public Pet? Pet { get; set; }
        public int ServiceId { get; set; }
        public PetService? Service { get; set; }
        public int CustomerId { get; set; }
        public User? Customer { get; set; }
        public DateTime AppointmentDate { get; set; }
        public string Status { get; set; } = "Pending"; // Pending, Confirmed, Completed, Cancelled
        public string Notes { get; set; } = string.Empty;
        public decimal TotalPrice { get; set; }
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }

    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Category { get; set; } = "Thức Ăn"; // Thức Ăn, Đồ Chơi, Phụ Kiện, Sức Khỏe
        public decimal Price { get; set; }
        public int StockQuantity { get; set; } = 50;
        public string Description { get; set; } = string.Empty;
        public string ImageUrl { get; set; } = string.Empty;
        public double Rating { get; set; } = 4.8;
    }

    public class ContactMessage
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Subject { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public bool IsRead { get; set; } = false;
    }

    // DTOs
    public class LoginDto
    {
        public string Email { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }

    public class RegisterDto
    {
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public string Role { get; set; } = "Customer";
    }

    public class OAuth2LoginDto
    {
        public string Provider { get; set; } = "Google";
        public string Email { get; set; } = string.Empty;
        public string FullName { get; set; } = string.Empty;
        public string AvatarUrl { get; set; } = string.Empty;
    }

    public class GoogleJwtLoginDto
    {
        public string IdToken { get; set; } = string.Empty;
    }

    public class AuthResponseDto
    {
        public string Token { get; set; } = string.Empty;
        public UserDto User { get; set; } = new UserDto();
    }

    public class UserDto
    {
        public int Id { get; set; }
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Role { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public string Address { get; set; } = string.Empty;
        public string AvatarUrl { get; set; } = string.Empty;
        public string OAuthProvider { get; set; } = string.Empty;
    }

    public class AppointmentCreateDto
    {
        public int PetId { get; set; }
        public int ServiceId { get; set; }
        public DateTime AppointmentDate { get; set; }
        public string Notes { get; set; } = string.Empty;
    }

    public class ProductOrder
    {
        public int Id { get; set; }
        public string CustomerName { get; set; } = string.Empty;
        public string CustomerPhone { get; set; } = string.Empty;
        public string ShippingAddress { get; set; } = string.Empty;
        public string PaymentMethod { get; set; } = "COD";
        public decimal TotalAmount { get; set; }
        public string Status { get; set; } = "Completed";
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }

    public class ProductCheckoutDto
    {
        public List<CartItemDto> Items { get; set; } = new List<CartItemDto>();
        public string CustomerName { get; set; } = string.Empty;
        public string CustomerPhone { get; set; } = string.Empty;
        public string ShippingAddress { get; set; } = string.Empty;
        public string PaymentMethod { get; set; } = "COD";
    }

    public class CartItemDto
    {
        public int Id { get; set; }
        public int Quantity { get; set; }
    }

    public class PagedResult<T>
    {
        public List<T> Items { get; set; } = new List<T>();
        public int TotalItems { get; set; }
        public int Page { get; set; }
        public int PageSize { get; set; }
        public int TotalPages => (int)Math.Ceiling((double)TotalItems / (PageSize > 0 ? PageSize : 1));
    }
}

