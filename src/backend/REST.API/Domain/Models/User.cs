using System.Collections.Generic;

namespace REST.API.Domain.Models
{
    public class User 
    {
        public int Id {get; set;}
        public string Name {get; set;}
        
        public string email {get; set;}
        public string password {get; set;}
        public IList<Message> Messages {get; set;} = new List<Message>();
        public IList<GroupMember> MemberOn {get; set;} = new List<GroupMember>();
    }
}