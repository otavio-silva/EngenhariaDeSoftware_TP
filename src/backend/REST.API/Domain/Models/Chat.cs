using System.Collections.Generic;

namespace REST.API.Domain.Models
{
    public class Chat 
    {
        public int Id {get; set;}
        public Group Group {get; set;}
        public bool IsGroup {get; set;}   
        public IList<Message> Messages {get; set;} = new List<Message>();
    }
}