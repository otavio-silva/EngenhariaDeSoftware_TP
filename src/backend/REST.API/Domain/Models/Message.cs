using System;

namespace REST.API.Domain.Models
{
    public class Message
    {
        public int Id {get; set;}
        public int ChatId {get; set;}
        public Chat Chat {get; set;}
        public int SenderId {get; set;}
        public User Sender {get; set;}

        public string Content {get; set;}
        public DateTime sent_at {get; set;}

        public DateTime received_at {get; set;}
        public DateTime read_at {get; set;}
    }
}