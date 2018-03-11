package skitter.auth;

import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.filter.AndFilter;
import org.springframework.ldap.filter.PresentFilter;
import org.springframework.web.bind.annotation.*;

@RestController
public class LDAPAuth {

    final private static String baseDn = "ou=People,dc=rit,dc=edu";

    @RequestMapping(value = "/signIn", method = RequestMethod.POST)
    @ResponseBody
    public String signIn(@RequestParam("username") String username, @RequestParam("password") String password) {
        LDAPConfiguration config = new LDAPConfiguration();
        config.setUsername("uid=" + username + "," + baseDn);
        config.setPassword(password);

        AndFilter filter = new AndFilter();
        filter.and(new PresentFilter("objectclass"));

        boolean authenticated = false;
        try {
            LdapTemplate template = config.ldapTemplate();
            authenticated = template.authenticate("uid=" + username + "," + baseDn, filter.encode(), password);
        } catch (Exception e) {
            authenticated = false;
            System.err.println(e.getMessage());
        }

        if (authenticated) {
            return "User authenticated.";
        }
        return "Screw you!";
    }

}
