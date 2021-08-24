import * as icons from '@material-ui/icons'

export class IconHook {
    static hook(iconName: string) {
        console.log(icons)
        // return null;
        return (icons as any)[iconName];
    }
}
