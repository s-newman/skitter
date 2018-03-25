package skitter.auth;

import org.springframework.ldap.core.AttributesMapper;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.filter.AndFilter;
import org.springframework.ldap.filter.PresentFilter;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.naming.NamingException;
import javax.naming.directory.Attributes;
import java.security.SecureRandom;
import java.sql.PreparedStatement;
import java.util.List;

@RestController
public class Controller {

    final private static String baseDn = "ou=People,dc=rit,dc=edu";
    final private static int tokenLength = 40;

    private static String generateSessionID() {
        SecureRandom rand = new SecureRandom();
        String token = "";
        for (int i = 0; i < tokenLength; i++) {
            token = token + Integer.toHexString(rand.nextInt(0x100));
        }
        return token;
    }

    @RequestMapping(value = "/signIn", method = RequestMethod.POST, produces = "application/json")
    public ResponseTransfer signIn(@RequestParam("username") String username, @RequestParam("password") String password) {

        LDAPConfiguration config = new LDAPConfiguration();
        config.setUsername("uid=" + username + "," + baseDn);
        config.setPassword(password);

        AndFilter filter = new AndFilter();
        filter.and(new PresentFilter("objectclass"));

        boolean authenticated;
        List<Person> people = null;

        try {
            LdapTemplate template = config.ldapTemplate();
            authenticated = template.authenticate("uid=" + username + "," + baseDn, filter.encode(), password);
            people = template.search("uid=" + username + "," + baseDn, filter.encode(), new PersonAttributesMapper());
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return new ResponseTransfer("unsuccessful", "", e.getMessage());
        }

        if (authenticated) {
            if (people == null) {
                return new ResponseTransfer("unsuccessful", "", "Cannot get user information");
            }

            System.out.println(people.get(0));
            PreparedStatement stmt = null;
            DB db = null;
            String sessionID = "";

            try {
                db = new DB("172.17.0.2:3306", "users");
                stmt = db.getConn().prepareStatement("INSERT INTO SESSION (rit_username, session_id) VALUES (?, ?)");
                stmt.setString(1, username);
                sessionID = generateSessionID();
                stmt.setString(2, sessionID);
                stmt.executeUpdate();
            } catch (Exception e) {
                return new ResponseTransfer("unsuccessful", "", "Error connecting to database");
            } finally {
                db.destroyConnection();
                try {
                    if (stmt != null) {
                        stmt.close();
                    }
                } catch (Exception e) {
                    return new ResponseTransfer("unsuccessful", "", "Cannot close statement");
                }
            }

            return new ResponseTransfer("successful", sessionID, "" + people.get(0));
        }
        return new ResponseTransfer("unsuccessful", "", "unknown error");
    }

    private class ResponseTransfer {

        private String success;
        private String sessionID;
        private String text;

        public ResponseTransfer(String success, String sessionID, String text) {
            this.success = success;
            this.sessionID = sessionID;
            this.text = text;
        }

        public String getSuccess() {
            return success;
        }

        public String getSessionID() {
            return sessionID;
        }

        public String getText() {
            return text;
        }
    }

    private class PersonAttributesMapper implements AttributesMapper<Person> {
        public Person mapFromAttributes(Attributes attrs) throws NamingException {
            Person person = new Person();
            person.setLastName((String) attrs.get("sn").get());
            person.setFirstName((String) attrs.get("givenName").get());
            return person;
        }
    }

    private class Person {
        private String firstName;
        private String lastName;

        public Person() {
        }

        public String getFirstName() {
            return firstName;
        }

        public void setFirstName(String firstName) {
            this.firstName = firstName;
        }

        public String getLastName() {
            return lastName;
        }

        public void setLastName(String lastName) {
            this.lastName = lastName;
        }

        @Override
        public String toString() {
            return "{" +
                    "\"firstName\": \"" + firstName + "\"" +
                    ", \"lastName\": \"" + lastName + "\"" +
                    '}';
        }
    }

}
